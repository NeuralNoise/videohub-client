'use strict';


angular.module('videohubClientApp.api', ['restangular', 'videohubClientApp.settings'])
  .factory('VideohubApi',
  function (Restangular, videohubApiBaseUrl, videohubSecretToken) {
    return Restangular.withConfig(function (RestangularConfigurer) {
      RestangularConfigurer.setRequestSuffix('');
      RestangularConfigurer.setBaseUrl(videohubApiBaseUrl);
      RestangularConfigurer.setDefaultHeaders({
        Authorization: 'Token ' + videohubSecretToken
      });
    });
  })
  .factory('VideoHubVideoApi', function (VideohubApi) {
    // the autocomplete widget likes it like this.
    return VideohubApi.all('videos');
  });
