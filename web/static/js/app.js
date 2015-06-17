// filters

var filters = angular.module('customFilters', []).filter('cut', function () {
    return function (input) {
        if (input.length > 50) {
            return input.slice(0, 49) + "..."
        }
        return input
    };
});

// Declaring main App
var app = angular.module('WikiAnalysisApp', ['customFilters'])

// Services

app.service('Socket', function () {
    namespace = '/wiki'; // change to an empty string to use the global namespace
    this.socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    this.on = function (event, callable) {
        this.socket.on(event, callable)
    }
    this.emit = function(name,data){
        this.socket.emit(name, data)
    }
});


// Controllers
app.controller('WikiNewDataController', function ($scope, Socket) {
    // create local variables
    $scope.activities = [];
    $scope.ldc = null;

    // methods
    $scope.updateActivities = function (data) {
            var maxArraySize = 15;
            $scope.activities.push(data);
            if ($scope.activities.length > maxArraySize) {
                $scope.activities.shift();
            }
            $scope.$apply();
        }
        // bind events to according functions
    Socket.on('server.data.new', $scope.updateActivities);
});

// Search Part
app.controller("WikiSearchDataController", function ($scope, Socket) {
    $scope.input = ""
    $scope.results = []

    $scope.search = function () {
        Socket.emit("client.search.request", $scope.input)
    }
    $scope.handleResults = function(data){
        $scope.results = data.hits.hits
        $scope.$apply()
    }
    Socket.on('server.search.result', $scope.handleResults);
});