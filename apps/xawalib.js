/*
 * XAWA Library
 *
 * Copyright 2010 - 2011, Tomáš Vaisar
 * tomas.vaisar@gmail.com, xvaisa00@stud.fit.vutbr.cz
 *
 * Released under GPL
 */

(function (window, document, undefined) {

	// encapsulating XAWA object
	var _x = function () { };

	_x.prototype = {
		// Dummy method, that tests if there's XAWA API present
		_init: function () {
			try {
				// let's call internal xawa init() method
				xawa.init();
			} catch (err) {
			// if initialization fails, there's no reason to continue
				window.stop();
				throw (err);//'Exception: XAWA initialization failed!' + err;
			}
		},

		//
		getVersion: function () {
			try {
				return xawa.getVersion();
			} catch (err) {
				throw err;
			}
		},

		//
		sendData: function (json_data, callback) {
			try {
				xawa.sendData(JSON.stringify(json_data));
				if (callback !== undefined) {
					callback();
				}
			} catch (err) {
				throw 'Exception: Given object is not valid JSON object!';
			}
		}
	};
	
	var X = new _x();

	// let's try to initialize it
	X._init();

	// remapping of the original 'xawa' object in 'window' scope
	window.xawa = X;//new _x();

})(this,this.document);
