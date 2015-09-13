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
    .otherwise({
            redirectTo: '/'
    });
});
    