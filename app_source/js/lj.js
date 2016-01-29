var $ = require('jquery');
var React = require('react');
var ReactDOM = require('react-dom');

var EntryList = React.createClass({
    render: function() {
        return (
            <div>This is the Entry List Component</div>
        )
    }
});

ReactDOM.render(
  <EntryList />,
  document.getElementById('content')
);

console.log('i am here');