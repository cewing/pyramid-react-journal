window.$ = require('jquery');
window.jQuery = window.$;
var Bootstrap = require('bootstrap');
var React = require('react');
var ReactDOM = require('react-dom');
var Lorem = require('react-lorem-component');
var HomePageContent = module.exports.HomePageContent = require('./modules/lj_pages').HomePageContent;
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

// var Entry = React.createClass({

//     getRandomIntInclusive: function(min, max) {
//       return Math.floor(Math.random() * (max - min + 1)) + min;
//     },

//     getDefaultProps: function() {
//         return {
//             sentenceLowerBound: 7,
//             sentenceUpperBound: 20,
//             paragraphLowerBound: 3,
//             paragraphUpperBound: 10
//         };
//     },

//     render: function() {
//         return (
//             <article>
//                 <h2>An Entry</h2>
//                 <Lorem {...this.props} count={this.getRandomIntInclusive(3, 8)} random={this.getRandomIntInclusive(1, 100000)}/>
//             </article>
//         );
//     }
// })


// var EntryList = React.createClass({
//     getDefaultProps: function() {
//         return {entryCount: 10};
//     },

//     render: function() {
//         var entries = [];
//         for (var i = 0; i < this.props.entryCount; i++) {
//             entries.push(<Entry key={i} />)
//         }
//         return (
//             <div>
//                 {entries}
//             </div>
//         );
//     }
// });

// var SideBarPanel = React.createClass({
//     render: function() {
//         return (
//             <div className="panel panel-default">
//                 <div className="panel-heading">
//                     <h3 className="panel-title">Sidebar Panel</h3>
//                 </div>
//                 <div className="panel-body">
//                     <ul>
//                         <li><a href="#">A Linked List Entry</a></li>
//                     </ul>
//                 </div>
//             </div>
//         );
//     }
// });

// var HomePageContent = React.createClass({
//     render: function() {
//         return (
//             <div className="row">
//                 <div className="page-header col-sm-12">
//                     <h1>Today I Learned &hellip; <small>401 Python learning Journal</small></h1>
//                 </div>
//                 <main className="col-sm-9">
//                     <EntryList />
//                 </main>
//                 <aside className="col-sm-3">
//                   <SideBarPanel />
//                 </aside>
//             </div>
//         )
//     }
// });

// ReactDOM.render(
//   <HomePageContent />,
//   document.getElementById('content')
// );



console.log('i am here');