/*
 * XAWA Library
 *
 * Created by Tomáš Vaisar, 2011
 * tomas.vaisar@gmail.com, xvaisa00@stud.fit.vutbr.cz
 *
 * Released under GNU/LGPL
 */

/*
 * Following event are fired from browser (XAWA plugin window)
 */
function onApplicationReady() {
	alert("If this message shows up (which it shouldn't), please right click in the window and hit 'Reload'. This message shouldn't be displayed again. If it is ... I'm doomed.")
	throw('Exception: onApplicationReady not implemented!');
}

function onInvitationAccept() {
	throw('Exception: onInvitationAccept not implemented!');
}

function onInvitationRefuse() {
	throw('Exception: onInvitationRefuse not implemented!');
}

function onMessageReceived(msg) {
	throw('Exception: onMessageReceived not implemented!');
}

function onDataReceived(data) {
	throw('Exception: onDataReceived not implemented!');
}

function onSessionLeave() {
	throw('Exception: onSessionLeave not implemented!');
}

(function (window, document, undefined) {

	var __xawa = window.xawa;

	// encapsulating XAWA object
	var _x = function () { };

	_x.prototype = {
		// Dummy method, that tests if there's XAWA API present
		_init: function () {
			try {
				// let's call internal xawa init() method
				__xawa.init();
			} catch (err) {
			// if initialization fails, there's no reason to continue
				window.stop();
				throw ('Exception: XAWA initialization failed!');
			}
		},

		//
		version: (function () {
			return __xawa.getXawaVersion();
		})(),

		// read-only property
		recipient: (function () {
			return __xawa.getRecipient();
		})(),

		//
		sendMessage: function(message, options) {
			try {
				if (options !== undefined) {
					if (options.messageType == 'classic')
						__xawa.sendClassicMessage(message);					
				} else {
					__xawa.sendMessage(message);
				}
			} catch (err) {
				throw ('Exception: Message could not be sent! ' + err);
			}
		},

		//
		sendData: function (json_data, options) { //onDataAcceptCallback) {
			try {
				if (options !== undefined) {
					if (options.mode == 'legacy')
						__xawa.sendDataInLegacyMode(JSON.stringify(json_data));
				} else {
					__xawa.sendData(JSON.stringify(json_data));					
				}					
			} catch (err) {
				throw ('Exception: Given object cannot be transformed to JSON object!');
			}
		},

		// invite
		invite: function (jid, appConfig, callbacks) {
			try {
				__xawa.sendInvite(jid === undefined ? __xawa.getRecipient() : jid, JSON.stringify(appConfig));
				// register callbacks on 'events'
				if (callbacks !== undefined) {
					if (callbacks.onAccept !== undefined)
						onInvitationAccept = callbacks.onAccept;
					if (callbacks.onRefuse !== undefined)
						onInvitationRefuse = callbacks.onRefuse;
				}
			} catch (err) {
				throw ('Exception: Invitation could not be sent! ' + err);
			}
		},
		
		// leave
		leave: function () {
			try {
				__xawa.leave();
			} catch (err) {
				throw ('Exception: Session could not be leaved! ' + err);
			}
		},		
	};
	
	var X = new _x();

	// let's try to initialize it
	X._init();

	// remapping of the original 'xawa' object in 'window' scope
	window.xawa = X;

})(this,this.document);
