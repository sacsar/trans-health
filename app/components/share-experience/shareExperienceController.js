transHealthApp.controller('shareExperienceController', function ($scope, $location, $http){
	//var experienceService = shareExperienceService;

	$scope.err = false;
	$scope.status = {};
	$scope.status.opened = false;

	$scope.state = ''
	$scope.company = ''
	$scope.plan = ''
	$scope.ages = _.range(1, 100)
	$scope.ages.push('100+')
	$scope.age = 18

	$scope.services = ['Cyproterone',
					   'Spironolactone',
					   'Finasteride',
					   'Estradiol',
					   'Testosterone',
					   'GnRH analogue',
					   'Facial Feminization',
					   'Mastectomy',
					   'Phalloplasty',
					   'Vaginaplasty',
					   'Labiaplasty',
					   'Breast Augmentation',
					   'Orchiectomy',
					   'Hystorectomy',
					   'Oophorectomy',
					   'Metoidioplasty',
					   'Therapy',
					   'Voice Training']

	$scope.open = function($event) {
    	$scope.status.opened = true;
  	};

  	$scope.submitexperience = function(){
  		params = {date: $scope.date,
  				  plan: $scope.plan,
  				  company: $scope.company,
  				  gender: $scope.gender,
  				  service: $scope.service,
  				  outcome: $scope.outcome,
  				  age: $scope.age
  				}
  		postExperience(params)
  	}

  	// this should be factored out as a service, but right now it's busted
  	var postExperience = function(params){
  		payload = {
  				   company: params.company,
  				   plan: params.plan,
  				   state: params.state,
  				   services: [{name: params.service,
  				   			   date: params.date,
  				   			   gender: params.gender,
  				   			   success: params.outcome,
  				   			   age: params.age
  				   			  }]
  				}

  		$http.post('/api/v1/experience', payload)
  	};
});