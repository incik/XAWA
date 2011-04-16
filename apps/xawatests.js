/*
 * XAWA Library Tests
 *
 *
 */
 
(function(window, document, undefined) {

	var _xawaTests = function () {};
	var _successed = 0;
	var _failed = 0;
	_xawaTests.prototype = {

		can_be_initialized : function() {
			try {
				xawa._init();
				_successed++;
			} catch (err) {
				_failed++;
				throw (err);
			}
		},

	};

	var Tests = new _xawaTests();
	try {
		Tests.can_be_initialized();
		alert('success');
	} catch (err) {
		alert(err);
	}
 
	/*for (var test in Tests) {
		try {
		Tests[test]();
		}
		catch (err) {
			alert(err);
		}
	}*/

	//alert(Tests.length + ' tests runned');

})(this, this.window);
