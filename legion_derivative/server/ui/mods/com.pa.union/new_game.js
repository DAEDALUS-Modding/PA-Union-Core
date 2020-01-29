//START - moar code appropriated from Legion for yellow commander select
var unionLoaded;

if (!unionLoaded) {

    unionLoaded = true;

    function loadUnion() {

        var unionEnabled;

        model.enableUnion = function () {

            if (unionEnabled) {
                return;
            }

            unionEnabled = true;

            loadCSS('coui://ui/mods/com.pa.union/css/union_commander_picker.css');

            var unioncommander = ['/pa/units/commanders/union_valiant/union_valiant.json'];

            model.isNotUnion = function (commander, isEmpty) {
              if (!isEmpty) {
                return !_.includes(unioncommander, commander);
              }
              else {
                return true;
              }
            }
            
            model.isMLA = function (commander, isEmpty) {
              if (!isEmpty) {
                return !_.includes(unioncommander, commander);
              }
            }

            //Style Commander Picker Legion
            $('#commander-picker .div-commander-picker-item.btn_std_ix').attr("data-bind", "css: {unioncommander:!model.isNotUnion($data)}, click: function () { model.setCommander($index()) }, click_sound: 'default', rollover_sound: 'default'");
            $('#ai-commander-picker .div-commander-picker-item.btn_std_ix').attr("data-bind", "css: {unioncommander: !model.isNotUnion($data)}, click: function () { model.setAICommander(model.selectedAI(), $data) }, click_sound: 'default', rollover_sound: 'default'");
            
            $('.slot-player').attr("data-bind", "css: {unionslot: !model.isNotUnion($data.commander(),$data.isEmpty()), mlaslot: model.isMLA($data.commander(),$data.isEmpty()), ready: isReady, loading: isLoading}");
        }
        
        model.enableUnion();
    }

    try {
        loadUnion();
    } catch (e) {
        console.error(e);
    }
}
//END


model.localChatMessage(loc("!LOC:Union Expansion (EARLY TESTING)"), loc("!LOC:currently a work in progress."));
