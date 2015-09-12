transHealthApp.config(function($routeProvider) {
    $routeProvider
    .when ('/', {
        templateUrl: 'app/components/search/search.html',
        controller: 'searchController'
    })
    .when ('/results/:state/:query?', {
        templateUrl: 'app/components/results/results.html',
        controller: 'resultsController',
        reloadOnSearch: false
    })
    .when('/share/plan', {
        templateUrl: 'app/components/share-plan/share-plan.html',
    })
    .otherwise({
            redirectTo: '/'
    });
});
    