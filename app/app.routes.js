transHealthApp.config(function($routeProvider) {
    $routeProvider
    .when ('/', {
        templateUrl: 'app/components/search/search.html',
        controller: 'searchController'
    })
    .when('/report/plan', {
        templateUrl: 'app/components/report-plan/report-plan.html',
    })
    .otherwise({
            redirectTo: '/'
    });
});
    