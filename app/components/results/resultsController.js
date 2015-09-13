transHealthApp.controller('resultsController', function ($scope, $routeParams, resultsService) {
    console.log($routeParams)
    resultsService.getPlans($routeParams.state).then(function (resp){
        $scope.results = resp.data;
        console.log(resp.data)
    });
});