app
/**
 * Controller per il salvataggio del progetto corrente
 * @module saveProject
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $http Il servizio AngularJS {@link https://docs.angularjs.org/api/ng/service/$http|$http} per la
 * comunicazione con i server HTTP
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("saveProject", function ($scope, $http, $mdDialog, Labels) {

    $scope.saveGraph = function() {
        $http.post("../save_graph/", JSON.stringify(Labels))
            .then(function successCallback(response){
                console.log("Successfully POST-ed data to save_graph");
                }, function errorCallback(response){
                console.log("POST-ing of data failed to save_graph");
            });
	};

    /**
     * Salva i dati inviandoli alla view create_schema_NEO4J o alla view create_schema_SQL a seconda del DBMS
     * @function salvataggio
     */

    $scope.generateSchemaDB= function($event) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/generateSchemaDBModal.html',
            windowClass: 'modal-content',
            controller: generateSchemaDBCtrl,
            clickOutsideToClose: true
        });
    };

    function generateSchemaDBCtrl($scope, $mdDialog, Labels) {

        $scope.nomeProgetto = Labels.nomeProgetto;
        $scope.nomeDB = Labels.nomeDB;
        $scope.descrizioneProgetto = Labels.descrizioneProgetto;
        $scope.supportedDB = Labels.supportedDB;
        $scope.dbms = Labels.dbms;

        console.log($scope.dbms);
        console.log(Labels);

        $scope.create_schema = function () {
            data = {
                nomeDB: $scope.nomeDB,
                dbms: $scope.dbms,
                graph: Labels};

            if ($scope.dbms === 'Neo4j')
                $http.post("../create_schema_NEO4J/", JSON.stringify(data))
                    .then(function successCallback(response) {
                        console.log("Successfully POST-ed data to create_schema_NEO4J");
                    }, function errorCallback(response) {
                        console.log("POST-ing of data failed to create_schema_NEO4J");
                    });
            else if ($scope.dbms === "MySQL" || $scope.dbms === "SQLite")
                $http.post("../create_schema_SQL/", JSON.stringify(data))
                    .then(function successCallback(response) {
                        console.log("Successfully POST-ed data to create_schema_SQL");
                    }, function errorCallback(response) {
                        console.log("POST-ing of data failed to create_schema_SQL");
                    });
            $scope.closeDialog();
        };

        $scope.closeDialog = function () {
            $mdDialog.hide();
        };
    }
});