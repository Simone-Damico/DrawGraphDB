app
/**
 * Controller per la gestione dei nodi e la visualizzazione delle loro informazioni
 * @module nodeController
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("nodeController", function($scope, $mdDialog, Labels){
    
    $scope.showNodes = function ($event) {
        
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/showNodesModal.html',
            controller: nodesListCtrl,
            parent: angular.element(document.body),
            clickOutsideToClose: true
        });
    };
    
    function nodesListCtrl($scope, $mdDialog, Labels) {
        $scope.nodes = Labels.nodes;

        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        };
    }
    
    /**
     * Mostra la finestra modale per la visualizzione delle informazioni del nodo cliccato dall'utente
     * @function showNodeInfo
     * @param {event} $event Click dell'utente sul nodo nel grafo
     */
    $scope.showNodeInfo = function(nodo, $event) {

        $mdDialog.show({
            locals:{nodo: nodo},
            targetEvent: $event,
            templateUrl: 'static/source/templates/nodeModal.html',
            controller: nodeCtrl,
            parent: angular.element(document.body),
            clickOutsideToClose: true
        });
    };

    // funzione che gastisce il modal
	function nodeCtrl($scope, $mdDialog, Labels, nodo) {

	    $scope.nodo = nodo;
        $scope.domini = Labels.domini;
        $scope.pk = null;

        $scope.genericoProp = function () {
            $scope.domini.forEach(function (value) {
                if (value.nome === $scope.nodo.proprieta[$scope.indexProp].dominio){
                    $scope.generico = value.generico;
                }
            });
        };

        /**
         * Resetta i campi default e degli intervalli
         * @function resetDom
         * @param {Number} ind Indice del nodo selezionato
         */
        $scope.resetDom = function (ind) {
            $scope.nodo.proprieta[ind].default = null;
            $scope.nodo.proprieta[ind].intervalli = [];
            $scope.indexProp = undefined;
        };

        /**
         * Aggiunge una nuova proprietà a quelle del nodo selezionato
         * @function addNodeProp
         */
        $scope.addNodeProp = function () {
            console.log("ADD NODE PROP");
            var keepGoing = true;

            // Se il nome della propietà non è stato inserito --> allert
            if ($scope.newNodeProp.nome === undefined || $scope.newNodeProp.nome === '' || $scope.newNodeProp.nome === null) {
                alert("Inserire il nome della proprietà");
                return;
            }

            // Controllo se il nome della proprietà esisste gia --> allert
            $scope.nodo.proprieta.forEach(function (element) {
                if (element.nomeProp === $scope.newNodeProp.nome) {
                    alert("La proprietà esiste già");
                    keepGoing = false;
                }
            });
            // Se la proprietà non esiste già (unicità del nome) --> la inserisco
            if (keepGoing)
                $scope.nodo.proprieta.push(
                    {nomeProp: $scope.newNodeProp.nome,
                        dominio: $scope.newNodeProp.dominio,
                        notNull: $scope.newNodeProp.notNull,
                        default: null,
                        intervalli:[]});
            console.log($scope.newNodeProp.notNull);
            $scope.newNodeProp.nome = undefined;
            $scope.newNodeProp.dominio = undefined;
        };

        /**
         * Rimuove la proprietà con indice ind tra quelle del nodo selezionato
         * @function removeNodeProp
         * @param {Number} ind Indice della proprietà da eliminare
         */
        $scope.removeNodeProp = function (ind) {
            $scope.nodo.proprieta.splice(ind, 1);
        };

        /**
         * Aggiunge un nuovo intervallo per i valori della proprietà selezionata
         * @function insIntervallo
         */
        $scope.insIntervallo = function () {
            //controllo estremi e definizione dell'intervallo
            if ($scope.sceltaVinc === "intervallo"){
                if ($scope.interDa == null || $scope.interA == null|| $scope.interDa === "" || $scope.interA === "") return;
                if ($scope.interDa <= $scope.interA) {
                    if ($scope.estremoDaIncl && $scope.estremoAIncl) var intervallo = "value >= " + $scope.interDa + " and value <= " + $scope.interA;

                    else if ($scope.estremoDaIncl && !$scope.estremoAIncl) var intervallo = "value >= " + $scope.interDa + " and value < " + $scope.interA;

                    else if (!$scope.estremoDaIncl && $scope.estremoAIncl) var intervallo = "value > " + $scope.interDa + " and value <= " + $scope.interA;

                    else var intervallo = "value > " + $scope.interDa + " and value < " + $scope.interA;
                }else{
                    alert("L'estremo inferiore deve essere minore o uguale di quello superiore");
                    return
                }
            }
            else if ($scope.sceltaVinc === "maggiore"){
                if ($scope.magDi == null|| $scope.magDi === "") return;
                if ($scope.estremoMag) var intervallo = "value >= " + $scope.magDi;
                else var intervallo = "value > " + $scope.magDi;
            }
            else if ($scope.sceltaVinc === "minore"){
                if ($scope.minDi == null || $scope.minDi === "") return;
                if ($scope.estremoMin) var intervallo = "value <= " + $scope.minDi;
                else var intervallo = "value < " + $scope.minDi;
            }

            // se il nuovo intervallo è gia presente non si inserisce
            if (($scope.nodo.proprieta[$scope.indexProp].intervalli.length === 0 ||
                !$scope.nodo.proprieta[$scope.indexProp].intervalli.includes(intervallo)) &&
                ($scope.interDa !== undefined || $scope.interA !== undefined || $scope.magDi !== undefined || $scope.minDi !== undefined))
                $scope.nodo.proprieta[$scope.indexProp].intervalli.push(intervallo);

            //reset campi degli intervalli
            $scope.interDa = null;
            $scope.estremoDaIncl = false;
            $scope.interA = null;
            $scope.estremoAIncl = false;
            $scope.magDi = null;
            $scope.estremoMag = false;
            $scope.minDi = null;
            $scope.estremoMin = false;
        };

        /**
         * Rimuove intervallo per i valori con indice ind della proprietà selezionata
         * @function removeIntervallo
         * @param {Number} ind Indice dell'intervallo da eliminare
         */
        $scope.removeIntervallo = function (ind) {
            $scope.nodo.proprieta[$scope.indexProp].intervalli.splice(ind, 1);
        };

        /**
         * Aggiunge la chiave primaria alla proprietà selezionata
         * @function addPK
         */
        $scope.addPK = function () {
            if ($scope.nodo.secondarykey.length > 0){

                $scope.nodo.secondarykey.forEach(function (chiave) {
                    chiave.forEach(function (value) {
                        if (value === $scope.pk) {
                            alert("non puoi scegliere come chiave primaria una proprietà che è gia chaive secondaria");
                            $scope.pk = undefined;
                        }
                    })
                })
            }
            else $scope.nodo.primaryKey = $scope.pk;
            console.log($scope.nodo.primaryKey);
            console.log($scope.pk);
            console.log(Labels)
        };

        /**
         * Aggiunge la chiave secondaria alla proprietà selezionata
         * @function addSK
         */
        $scope.addSK = function () {
            $scope.nodo.secondarykey.push($scope.altraChiave);
            $scope.altraChiave = undefined;
        };

        /**
         * Rimuove la chiave secondaria dalla proprietà selezionata
         * @function removeSK
         * @param {Number} ind Indice della chiave secondaria da eliminare
         */
        $scope.removeSK = function (ind) {
            $scope.nodo.secondarykey.splice(ind, 1);
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