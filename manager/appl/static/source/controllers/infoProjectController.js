app
/**
 * Controller per la visualizzazione delle informazioni del progetto corrente
 * @module infoProject
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $http Il servizio AngularJS {@link https://docs.angularjs.org/api/ng/service/$http|$http} per la
 * comunicazione con i server HTTP
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("infoProject", function($scope, $http, $mdDialog, Labels){

    $scope.labels = Labels;
    $scope.nomeProgetto = Labels.nomeProgetto;

    /**
     * Mostra la finestra modale per la visualizzione delle informazioni del
     * progetto corrente
     * @function showInfoProject
     * @param {event} $event Click dell'utente sul bottone dell'interfaccia
     */
    $scope.showInfoProject = function($event) {

        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/infoProjectModal.html',
            windowClass: 'modal-content',
            controller: projectInfoCtrl,
            clickOutsideToClose: true
        });
    };

    function projectInfoCtrl($scope, $mdDialog, Labels) {

        $scope.nomeProgetto = Labels.nomeProgetto;
        console.log($scope.nomeProgetto);
        $scope.nomeDB = Labels.nomeDB;
        $scope.descrizioneProgetto = Labels.descrizioneProgetto;
        $scope.supportedDB = Labels.supportedDB;
        $scope.dbms = Labels.dbms;

        /**
         * Modifica delle informazioni del progetto corrente,
         * invia i dati alla view change_project_data
         * @function modifica
         */
        $scope.modifica = function () {
            info = {
                nome: $scope.nomeProgetto,
                nomeDB: $scope.nomeDB,
                dbms: $scope.dbms,
                descrizione: $scope.descrizioneProgetto};
            $http.post("../change_project_data/", JSON.stringify(info))
                .then(function successCallback(response){
                    Labels.nomeProgetto = $scope.nomeProgetto;
                    Labels.nomeDB = $scope.nomeDB;
                    Labels.descrizioneProgetto = $scope.descrizioneProgetto;
                    Labels.dbms = $scope.dbms;
                    console.log("Successfully POST-ed data");
                    }, function errorCallback(response){
                    console.log("POST-ing of data failed");
            });
        };

        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        };
    }

});