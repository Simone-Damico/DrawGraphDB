app
/**
 * Controller per la gestione dei link e la visualizzazione delle loro informazioni
 * @module linkController
 * @param {Object} $scope L'oggetto {@link https://docs.angularjs.org/guide/scope|$scope} indica il contesto in cui sono
 * salvati i dati e valutate le espressioni
 * @param {Object} $mdDialog Il servizio di AngularJS Material
 * {@link https://material.angularjs.org/1.1.6/api/service/$mdDialog|$mdDialog} permette di gestire una finestra di
 * dialogo con l'utente
 * @param {Object} Labels Il servizio {@link Labels} contiene i dati del grafo utente
 */
.controller("linkController", function($scope, $mdDialog, Labels){

    $scope.links = Labels.links;

    $scope.showLinks = function ($event) {

        $mdDialog.show({
            targetEvent: $event,
            templateUrl: 'static/source/templates/showLinksModal.html',
            controller: linksListCtrl,
            parent: angular.element(document.body),
            clickOutsideToClose: true
        });
    };

    function linksListCtrl($scope, $mdDialog, Labels) {
        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        };
    }

    /**
     * Mostra la finestra modale per la visualizzione delle informazioni del link cliccato dall'utente
     * @function showLinkInfo
     * @param {event} $event Click dell'utente sul link nel grafo
     */
    $scope.showLinkInfo = function(link, $event) {
        $mdDialog.show({
            locals:{link: link},
            targetEvent: $event,
            templateUrl: 'static/source/templates/linkModal.html',
            windowClass: 'modal-content',
            controller: LinkCtrl,
            clickOutsideToClose: true
        });
    };

    function LinkCtrl($scope, $mdDialog, Labels, link) {

        $scope.link = link;
        $scope.domini = Labels.domini;
        $scope.molteplicita = Labels.molteplicita;
        $scope.pk = null;

        $scope.genericoProp = function () {
            $scope.domini.forEach(function (value) {
                if (value.nome === $scope.linkSelezionato.proprieta[$scope.indexProp].dominio){
                    $scope.generico = value.generico;
                }
            });
        };

        /**
         * Resetta i campi default e degli intervalli
         * @function resetDom
         * @param {Number} ind Indice dell'arco selezionato
         */
        $scope.resetDom = function (ind) {
            $scope.nodoSelezionato.proprieta[ind].default = null;
            $scope.nodoSelezionato.proprieta[ind].intervalli = [];
            $scope.indexProp = undefined;
        };

        /**
         * Aggiunge una nuova proprietà a quelle dell'arco selezionato
         * @function addLinkProp
         */
        $scope.addLinkProp = function () {

            var keepGoing = true;
            // Controllo se il nome della proprietà esisste gia --> allert
            $scope.linkSelezionato.proprieta.forEach(function (element) {
                if (element.nomeProp === $scope.newLinkProp.nome) {
                    alert("La proprietà esiste già");
                    keepGoing = false;
                }
            });
            // Se la proprietà non esiste --> la inserisco
            if (keepGoing) {
                $scope.linkSelezionato.proprieta.push(
                    {nomeProp: $scope.newLinkProp.nome,
                        dominio: $scope.newLinkProp.dominio,
                        notNull: $scope.notNull,
                        default: null,
                        intervalli:[]}
                );
            }
        };

        /**
         * Rimuove la proprietà con indice ind tra quelle dell'arco selezionato
         * @function removeLinkProp
         * @param {Number} ind Indice della proprietà da eliminare
         */
        $scope.removeLinkProp = function (ind) {
            $scope.linkSelezionato.proprieta.splice(ind, 1);
        };

        /**
         * Aggiunge un nuovo intervallo per i valori della proprietà selezionata
         * @function insIntervallo
         */
        $scope.insIntervallo = function () {
            //controllo estremi e definizione dell'intervallo
            if ($scope.sceltaVinc === "intervallo"){

                if ($scope.interDa == null || $scope.interA == null || $scope.interDa === "" || $scope.interA === "") return;

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
                if ($scope.magDi == null || $scope.magDi === "") return;
                if ($scope.estremoMag) var intervallo = "value >= " + $scope.magDi;
                else var intervallo = "value > " + $scope.magDi;
            }
            else if ($scope.sceltaVinc === "minore"){
                if ($scope.minDi == null || $scope.minDi === "") return;
                if ($scope.estremoMin) var intervallo = "value <= " + $scope.minDi;
                else var intervallo = "value < " + $scope.minDi;
            }

            // se il nuovo intervallo è gia presente non si inserisce
            if (($scope.linkSelezionato.proprieta[$scope.indexProp].intervalli.length === 0 ||
                    !$scope.linkSelezionato.proprieta[$scope.indexProp].intervalli.includes(intervallo)) &&
                ($scope.interDa !== undefined || $scope.interA !== undefined || $scope.magDi !== undefined || $scope.minDi !== undefined))
                $scope.linkSelezionato.proprieta[$scope.indexProp].intervalli.push(intervallo);

            //reset campi degli intervalli
            $scope.interDa = null;
            $scope.estremoDaIncl = false;
            $scope.interA = null;
            $scope.estremoAIncl = false;
            $scope.magDi = null;
            $scope.estremoMag = false;
            $scope.minDi = null;
            $scope.estremoMin = false;
            console.log($scope.linkSelezionato);
        };

        /**
         * Rimuove intervallo per i valori con indice ind della proprietà selezionata
         * @function removeIntervallo
         * @param {Number} ind Indice dell'intervallo da eliminare
         */
        $scope.removeIntervallo = function (ind) {
            $scope.linkSelezionato.proprieta[$scope.indexProp].intervalli.splice(ind, 1);
        };

        /**
         * Aggiunge la chiave secondaria alla proprietà selezionata
         * @function addSK
         */
        $scope.addSK = function () {
            $scope.linkSelezionato.secondarykey.push($scope.altraChiave);
            $scope.altraChiave = undefined;
        };

        /**
         * Rimuove la chiave secondaria dalla proprietà selezionata
         * @function removeSK
         * @param {Number} ind Indice della chiave secondaria da eliminare
         */
        $scope.removeSK = function (ind) {
            $scope.linkSelezionato.secondarykey.splice(ind, 1);
        };

        /**
         * Nasconde la finestra modale
         * @function closeDialog
         */
        $scope.closeDialog = function () {
            $mdDialog.hide();
        }
    }
});