angular.module('httpExample', []).config(function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })
    .controller('FetchController', ['$scope', '$http',
    function($scope, $http) {
/*
    $scope.getRequest = function () {
        console.log("I've been pressed!");
        $http.get("../post_list")
            .then(function successCallback(response){
                $scope.response = response;
                console.log($scope.response.data);
            }, function errorCallback(response){
                console.log("Unable to perform get request");
            });
    };*/

    $scope.postRequest = function () {
        $http.post("../prova_post/", {nome: "ciaoaiosm", 'csrfmiddlewaretoken':"{{ csrf_token }}"})
            .then(function successCallback(response){
                console.log("Successfully POST-ed data");
            }, function errorCallback(response){
                console.log("POST-ing of data failed");
            });
    };

  }]);