transHealthApp.controller('shareExperienceController', function ($scope, $location, $http, $modal){
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
  		console.log("submit experience")
  		params = {date: moment($scope.date).format('YYYY-MM-DD'),
  				  plan: $scope.plan,
  				  company: $scope.company,
  				  gender: $scope.gender,
  				  service: $scope.service,
  				  outcome: $scope.outcome,
  				  age: $scope.age,
  				  state: $scope.state
  				}
  		postExperience(params)
  			.success(function(resp){$scope.open(true)})
  			.error(function(){$scope.open(false)})
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
  				   			   success: params.outcome == 'yes',
  				   			   age: params.age
  				   			  }]
  				}
  		console.log(payload)
  		return $http.post('/api/v1/experience', payload)
  	};

  	//model stuff, should be a directive 
	  $scope.animationsEnabled = true;

  $scope.open = function (outcome) {

  	console.log("Open" + outcome)

    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ModalInstanceCtrl',
      resolve: {
        success: function() {return outcome }
        }
    });

    modalInstance.result.then(function (success) {
    	$scope.success = success
    }, function () {
    });
  };
});