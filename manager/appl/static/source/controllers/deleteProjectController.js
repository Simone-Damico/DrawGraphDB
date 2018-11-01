app

/**
 * Controller per l'eliminazione del progetto corrente
 * @module deleteProject
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $http Il servizio AngularJS {@link https://docs.angularjs.org/api/ng/service/$http|$http} per la
 * comunicazione con i server HTTP
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("deleteProject", function ($scope, $http, Labels) {
    /**
     * Elimina il progetto corrente
     * @function eliminazione
     *
     */
    $scope.eliminazione = function() {
        $scope.dbms = Labels.dbms;
	    console.log(Labels.nomeProgetto);
	    $http.post("../delete_project/", JSON.stringify(Labels.nomeProgetto))
            .then(function successCallback(response){
            console.log("Successfully POST-ed data to create_schema_NEO4J");
            }, function errorCallback(response){
            console.log("POST-ing of data failed to create_schema_NEO4J");
            });
    };
});