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
    .when('/share/experience', {
        templateUrl: 'app/components/share-experience/share-experience.html',
        controller: 'shareExperienceController'
    })
    .otherwise({
            redirectTo: '/'
    });
});
    