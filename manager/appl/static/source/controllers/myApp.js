var app = angular.module('MyApp', ['ngAria', 'ngMaterial', 'ngMessages']).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });