transHealthApp.service('companiesService', function($http) {
	var service = {};

	service.getCompanies = function(){
		return $http.get('/api/v1/companies')
	}

	return service
});