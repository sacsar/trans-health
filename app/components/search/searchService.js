transHealthApp.service('searchService', function ($http) {
    var service = {};
    
    service.getPlan = function (company, name, state) {
    	var params = {}
    	params.state = state
    	params.dimension = 'plan'
    	params.values = [company, name]
        return this.searchPlan(params)
    }

    service.getPlansByCompany = function(company, state) {
    	var params = {}
    	params.dimenions = 'company'
    	params.values = [company]
    	params.state = state
    	return this.searchPlan(params)
    }

    service.getPlans = function(state){
    	var params = {}
    	params.state = state
    	return this.searchPlan(params)
    }

    service.searchPlan = function(params){
    	return $http.get('/api/v1/search/' + angular.element.param(params))
    }
    
    return service;
});