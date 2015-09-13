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
        templateUrl: 'app/components/share/share-plan.html',
        controller: 'sharePlanController'
    })
    .when('/share/experience', {
        templateUrl: 'app/components/share-experience/share-experience.html',
        controller: 'shareExperienceController'
    })
    .when('/faq', {
        templateUrl: 'app/components/faq/faq.html',
    })
    .otherwise({
            redirectTo: '/'
    });
});
    