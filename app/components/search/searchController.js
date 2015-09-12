transHealthApp.controller('searchController', function ($scope, $location) {
    $scope.err = false;
    
    $scope.search = function (state, query) {
//        if (state) {
//            if (query) {
//                $location.path('/results/' + state + '/' + query);
//            } else {
//                $location.path('/results/' + state + '/');
//            }
//        } else {
//            $scope.err = true;
//        }
        console.log('searched: ' + state + ' ' + query);
    }
});