transHealthApp.directive('resultExpand', function () {
    return {
        restrict: 'A',
        templateUrl: 'app/shared/directives/result-expand/result-expand.html',
        link: function (scope, element, attr) {
            element.find('.claims--expand').on('click', function () {
                $(this).parent().next().slideToggle('fast', 'swing');
                $(this).find('.glyphicon').toggleClass('claims--expand--icon__up');
            });
        }
    }
});