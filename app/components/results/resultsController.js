transHealthApp.controller('searchController', function ($scope, $location, resultsService) {
    
    resultsService.getPlans().then(function (resp){
        $scope.results = resp.data;
    });
});