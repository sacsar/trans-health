transHealthApp.controller('searchController', function ($scope, searchService) {
    $scope.getPlans = function () {
        searchService.getPlans().then(function(resp) {
            $scope.results = resp.data;
        });
    }
});