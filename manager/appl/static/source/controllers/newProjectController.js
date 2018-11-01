app
/**
 * Controller per la creazione di un nuovo progetto
 * @module newProject
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $http Il servizio AngularJS {@link https://docs.angularjs.org/api/ng/service/$http|$http} per la
 * comunicazione con i server HTTP
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("newProject", function ($scope, $http, $mdDialog, Labels) {

    $scope.labels = Labels;

    /**
     * Mostra la finestra modale per la creazione di un nuovo progetto
     * @function showNewProject
     * @param {event} $event Click dell'utente sul bottone dell'interfaccia
     */
    $scope.showNewProject = function ($event) {

		$mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/newProjectModal.html',
            windowClass: 'modal-content',
            controller: newProjectCtrl,
            clickOutsideToClose: true
        });
    };

	function newProjectCtrl($scope, $mdDialog, Labels) {

        $scope.supportedDB = Labels.supportedDB;

        // Meta informazioni sul progetto
        $scope.nomeProgetto = Labels.nomeProgetto;
        $scope.descrizioneProgetto = Labels.descrizioneProgetto;
        $scope.nomeDB = Labels.nomeDB;
        $scope.dbms = Labels.dbms;
        $scope.porta = Labels.porta;
        $scope.projectFolder = Labels.projectFolder;

        /**
         * Crea un nuovo progetto inviando i dati all view new_project
         * @function newProject
         */
        $scope.newProject = function () {
            info = {
                name: $scope.nomeProgetto,
                description: $scope.descrizioneProgetto};
            console.log(info);
            $http.post("../new_project/", JSON.stringify(info))
            .then(function successCallback(response){
                // Inizializzo le variabili di Labels con i dati del progetto appena creato
                Labels.nomeProgetto = response.data.name_project;
                Labels.nomeDB = response.data.name_db;
                Labels.dbms = response.data.dbms;
                Labels.porta = response.data.port;
                Labels.projectFolder = response.data.folder;
                Labels.createdDate = response.data.created_date;
                $scope.closeDialog();
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