'use strict';


angular.module('videohubClientApp.picker', ['videohubClientApp.api'])
  .directive('videohubVideoPicker', function () {
    return {
      restrict: 'E',
      templateUrl: '/cms/partials/directives/videohub-video-picker.html',
      scope: {
        video: '='
      },
      controller: function ($scope, VideohubApi) {
        $scope.selectedVideo = null;
        
        $scope.selectVideo = function (newVideo) {
          $scope.video = newVideo;
          $scope.selectedVideo = newVideo;
        }
        $scope.$watch('selectedVideo', function (newVal, oldVal) {
          if (newVal) {
            // extract some keywords for this video
            var keywords = [];
            if (newVal.channel) {
              keywords.push(newVal.channel.name);
              keywords.push(newVal.channel.description);
            }
            if (newVal.sponsor) {
              keywords.push(newVal.sponsor.name);
            }
            if (newVal.series) {
              keywords.push(newVal.series.name);
              keywords.push(newVal.series.description);
            }
            if (newVal.season) {
              keywords.push(newVal.season.name);
              keywords.push(newVal.season.number);
            }
            if (newVal.tags) {
              for (var i = 0; i < newVal.tags.length; i++) {
                keywords.push(newVal.tags[i]);
              }
            }
            keywords = keywords.join(' ');
            $scope.video = {
              id: newVal.id,
              title: newVal.title,
              description: newVal.description || "",
              keywords: keywords,
              image: null
            };
          }
        }); 
      }
    };
  });
