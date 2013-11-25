'use strict';

var contohApp = angular.module('contohApp', [
    'ngRoute'
]);

contohApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: 'static/templates/master-list.html',
            controller : 'ContohListCtrl'
        }).
        when('/new', {
            templateUrl: 'static/templates/new.html',
            controller : 'NewCtrl'
        }).
        when('/master/:master_id', {
            templateUrl: 'static/templates/new.html',
            controller : 'DetailCtrl'
        }).
        otherwise({
            redirectTo: '/'
        });
}]);

contohApp.controller('ContohListCtrl', function($scope, $http) { 
    $http.get('/master.json').success(function(data) {
        $scope.items = data.objects;
    });
});

contohApp.controller('NewCtrl', function($scope, $http, $location) {
    $scope.data = {name: '', items:[]};

    $scope.addItem = function() {
        $scope.data.items.push({name: $scope.itemName,
            qty: $scope.itemQty, price: $scope.itemPrice});
        $scope.itemName = '';
        $scope.itemQty = '';
        $scope.itemPrice = '';

        $('#itemName').focus();
    }

    $scope.sum = function() {
        var sum = 0;
        var i;

        for (i = 0; i < $scope.data.items.length; i++) {
            sum += $scope.data.items[i].qty * $scope.data.items[i].price;
        }
        return sum;
    }

    $scope.save = function() {
        $http.post('/master.json', $scope.data).success(function(data) {
            $location.path('/');
        }).error(function(data) {
            alert('Error');
        });
    }
});


contohApp.controller('DetailCtrl', function($scope, $http, $location, $routeParams) {
    $http.get('/master/' + $routeParams.master_id + '.json').success(function(data) {
        $scope.data = data;
    });

    $scope.addItem = function() {
        $scope.data.items.push({name: $scope.itemName,
            qty: $scope.itemQty, price: $scope.itemPrice});
        $scope.itemName = '';
        $scope.itemQty = '';
        $scope.itemPrice = '';

        $('#itemName').focus();
    }

    $scope.save = function() {
        $http.post('/master/' + $scope.data.id + '.json', $scope.data).success(function(data) {
            $location.path('/');
        }).error(function(data) {
            alert('Error');
        });
    }

    $scope.sum = function() {
        var sum = 0;
        var i;

        for (i = 0; i < $scope.data.items.length; i++) {
            sum += $scope.data.items[i].qty * $scope.data.items[i].price;
        }
        return sum;
    }

});
