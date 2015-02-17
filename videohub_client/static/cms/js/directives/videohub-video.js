'use strict';


angular.module('videohubClientApp.videoDirective', ['videohubClientApp.settings'])
  .directive('videohubVideo', function () {
    return {
      restrict: 'E',
      templateUrl: '/cms/partials/directives/videohub-video.html',
      scope: {
        video: '='
      },
      controller: function ($scope) {
      }
    };
  });
