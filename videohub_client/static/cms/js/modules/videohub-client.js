'use strict';

angular.module('videohubClientApp', [
  'videohubClientApp.api',
  'videohubClientApp.picker',
  'videohubClientApp.videoDirective'
]);

angular.module('videohubClientApp.settings', [])
  .constant('videohubApiBaseUrl', 'http://videohub.local/api/v0')
  .constant('videohubSecretToken', 'CONFIG IN YOUR SITE');
