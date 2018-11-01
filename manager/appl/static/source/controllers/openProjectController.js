app
/**
 * Controller per l'apertura di un nuovo progetto
 * @module openProject
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $http Il servizio AngularJS {@link https://docs.angularjs.org/api/ng/service/$http|$http} per la
 * comunicazione con i server HTTP
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("openProject", function($scope, $http, $timeout, $mdDialog, Labels){

    $scope.labels = Labels;
    $scope.progetti = null;

    /**
     * Mostra la finestra modale per l'apertuta di un nuovo progetto
     * @function showOpenProject
     * @param {event} $event Click dell'utente sul bottone dell'interfaccia
     */
    $scope.showOpenProject= function($event) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/openProjectModal.html',
            windowClass: 'modal-content',
            controller: openProjectCtrl,
            clickOutsideToClose: true
        });
    };

    function openProjectCtrl($scope, $mdDialog, Labels) {

        $scope.nomeProgetto = Labels.nomeProgetto;
        $scope.nomeDB = Labels.nomeDB;
        $scope.descrizioneProgetto = Labels.descrizioneProgetto;
        $scope.supportedDB = Labels.supportedDB;
        $scope.dbms = Labels.dbms;

        // GET dei vari progetti e le loro informazioni
        $http.get("../show_projects/")
            .then(function successCallback(response) {
                $scope.progetti = response.data;
                console.log("res, ", response.data);
                console.log("Successfully GET-ed data");
                },function errorCallback(response){
                console.log("GET-ing of data failed");
            });

        /**
         * Apre il progetto selezionato dall'utente ricevendolo dalla view openProject
         * @function openPro
         * @param {Object} pro Il progetto da aprire
         */
        $scope.openPro = function (pro) {
            $scope.name_project = pro.fields.name_project;

            $http.post("../openProject/", JSON.stringify($scope.name_project))
                .then(function successCallback(response){
                    var dati = response.data;
                    console.log(dati);
                    // Inizializzo le variabili di Labels con i dati del progetto appena creato
                    Labels.nomeProgetto = response.data.name_project;
                    Labels.nomeDB = dati.name_db;
                    Labels.dbms = dati.dbms;
                    Labels.porta = dati.port;
                    Labels.projectFolder = dati.folder;
                    Labels.createdDate = dati.created_date;
                    var graph = JSON.parse(dati.graph);
                    console.log(graph);
                    if (!graph){
                        Labels.nodes = graph.nodes;
                        Labels.links = graph.links;
                        Labels.domini = graph.domini;
                        Labels.lastNodeId = graph.lastNodeId;
                        Labels.lastLinkId = graph.lastLinkId;
                        Labels.tipiBase = graph.tipiBase;
                        Labels.operatoriConfronto = graph.operatoriConfronto;
                        Labels.molteplicita = graph.molteplicita;
                        Labels.supportedDB = graph.supportedDB;
                    }
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