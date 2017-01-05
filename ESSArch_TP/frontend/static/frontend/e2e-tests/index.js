'use strict';

describe('my app', function() {
    beforeEach(function() {
      browser.get('/');
    });

	it('should automatically redirect to /login when location hash/fragment is empty and not logged in', function() {
		expect(browser.getLocationAbsUrl()).toMatch("/login");
	});

	it('should render login box when user navigates to /login', function() {
		expect($('.login-box').isPresent()).toBe(true);
	});
});
