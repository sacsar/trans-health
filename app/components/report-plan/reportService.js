transHealthApp.service('reportService', function($http){
	var service = {};

	service.reportExperience = function(company, plan, state, gender, age, procedures){
		var payload = {};
		payload.company = company;
		payload.plan = plan;
		payload.state = state;
		payload.stated_gender = gender;
		payload.procedures = procedures
		
		return $http.post('/api/v1/experience', payload)
	}

	service.reportPlan = function(state, type, exclusions, company){
		var payload = {}
		payload.state = state;
		payload.type = type;
		payload.exclusions = exclusions;
		payload.company = company

		return $http.post('/api/v1/plan', payload)
	}
});