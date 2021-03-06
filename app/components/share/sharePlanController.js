transHealthApp.controller('sharePlanController', function($scope, $location, $http, $modal){
	$scope.err = false;

	$scope.state = '';
	$scope.company = '';
	$scope.plan = '';

	$scope.allExcluded = '';
	$scope.hormonesExcluded = '';
	$scope.surgeryExcluded = '';

	$scope.submitplan = function(){
		var hormones = '';
		var medication = '';
		if($scope.allExcluded == 'yes'){
			hormones = 'no';
			surgery = 'no';
		} else {
			switch($scope.hormonesExcluded){
				case 'yes':
					hormones = 'no';
					break;
				case 'no':
					hormones = 'yes';
					break;
				default:
					hormones = 'unknown';
					break;
			}

			switch($scope.surgeryExcluded){
				case 'yes':
					surgery = 'no';
					break;
				case 'no':
					surgery = 'yes';
					break;
				default:
					surgery = 'unknown';
			}
		}

		coverage_report = {
			'date': moment().format('YYYY-MM-DD'),
			'plan': $scope.plan,
			'company': $scope.company,
			'state': $scope.state,
			'service_types': [
				{'name': 'medication', 'covered': hormones},
				{'name': 'surgery', 'covered': surgery}
				]
		}

		postCoverage(coverage_report)
  			.success(function(resp){$scope.open(true)})
  			.error(function(){$scope.open(false)})
	}

	// this should be a service
	var postCoverage = function(payload){
		console.log(payload)
		return $http.post('/api/v1/coverage', payload)
	}

	// modal stuff, should be a directive

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