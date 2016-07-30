window.$ = require('jquery');
window.jQuery = window.$;
var Bootstrap = require('bootstrap');
var React = require('react');
var ReactDOM = require('react-dom');
var LJEntryList = module.exports.LJEntryList = require('./modules/lj_entries').LJEntryList;
var LJEntry = module.exports.LJEntry = require('./modules/lj_entries').LJEntry;

window.render_react = (function() {

    var inner_render_react = function($containers, cmp_name) {
        if ($containers === undefined) {
            $containers = $('[data-react-component]');
        }
        $containers.each(function() {
            var component_name = cmp_name || $(this).data('react-component');
            var props = $(this).data('react-props') || {};

            var component = module.exports[component_name];
            if (component === undefined) {
                throw "Component not defined: " + component_name;
            }
            var element = React.createElement(component, props);
            ReactDOM.render(element, $(this)[0]);
        });
    };

    // render react components on page load
    inner_render_react();
    return inner_render_react;

})();
