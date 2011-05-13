/*
 * XAWA Library
 *
 * Copyright 2010 - 2011, Tomáš Vaisar
 * tomas.vaisar@gmail.com, xvaisa00@stud.fit.vutbr.cz
 *
 * Released under GPL
 */

/*
 * Following event are fired from browser (XAWA plugin window)
 */
function onApplicationReady() {
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

/*function onDataAccepted() {
	throw('Exception: onDataRecieved not implemented!');
}*/

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
				throw (err);//'Exception: XAWA initialization failed!' + err;
			}
		},

		//
		getVersion: function () {
			try {
				return __xawa.getXawaVersion();
			} catch (err) {
				throw err;
			}
		},

		// read-only property
		recipient: (function () {
			return __xawa.getRecipient();
		})(),

		/*
		getMessage: function (callback) {
			try {
				if (callback !== undefined)
					onMessageReceived = callback;
			} catch(err) {
				alert(err);
			}
		},*/

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
				alert(err);
			}
		},

		/*
		getData : function(callback) {
			if (callback !== undefined) {
				onDataReceived = callback;
			}
		}*/

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
				throw 'Exception: Given object cannot be transformed to JSON object!';
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
				
			}
		},
		
		//
		/*negotiateGame: function() {
			try {
				__xawa.sendData(JSON.stringfy({ negotiate: true, player: 2 }));
			} catch(err) {
				alert(err);
			}
		},*/
	};
	
	var X = new _x();

	// let's try to initialize it
	X._init();

	// remapping of the original 'xawa' object in 'window' scope
	window.xawa = X;

})(this,this.document);
