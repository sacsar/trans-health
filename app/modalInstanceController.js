transHealthApp.controller('ModalInstanceCtrl', function ($scope, $modalInstance, success) {


  $scope.success = success;
  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});