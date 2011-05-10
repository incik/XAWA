/*
 * XAWA Library
 *
 * Copyright 2010 - 2011, Tomáš Vaisar
 * tomas.vaisar@gmail.com, xvaisa00@stud.fit.vutbr.cz
 *
 * Released under GPL
 */

(function (window, document, undefined) {

	var __xawa = window.xawa;

	// little helper
	function sleep(delay) {
		var start = new Date().getTime();
		while (new Date().getTime() < start + delay);
	}

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

		recipient: (function () {
			return __xawa.getRecipient();
		})(),

		//
		sendData: function (json_data, callback) {
			try {
				__xawa.sendData(JSON.stringify(json_data));
				if (callback !== undefined) {
					callback();
				}
			} catch (err) {
				throw 'Exception: Given object is not valid JSON object!';
			}
		},

		// invite
		invite: function (jid, appConfig, onAcceptCallback, onRefuseCallback) {
			try {
				__xawa.sendInvite(jid === undefined ? __xawa.getRecipient() : jid, JSON.stringify(appConfig));
				//sleep(10000);
				var tstint = setInterval(function() {
				var result = __xawa.getInvitationAnswer();
				if (result == true && onAcceptCallback !== undefined) {
					onAcceptCallback();
					clearInterval(tstint);
				} else if (onRefuseCallback !== undefined) {
					onRefuseCallback();
					clearInterval(tstint);
				}
				}, 1000);
				
				/*var timeout = 10000;
				var timer;
				var answer = (function __getInvitationAnswer() {
					if (timeout == 0) {
						clearTimeout(timer);
						return undefined;
					}
					if (__xawa.invitationAnswer != '') {
						clearTimeout(timer);
						return __xawa.invitationAnswer;
					}
					timeout--;
					timer = setTimeout(function () { __getInvitationAnswer() }, 30000);
				})();

				if (answer === undefined) {
					alert('xxxx');
				}*/
			} catch (err) {
				
			}
		},
	};
	
	var X = new _x();

	// let's try to initialize it
	X._init();

	// remapping of the original 'xawa' object in 'window' scope
	window.xawa = X;//new _x();

})(this,this.document);
