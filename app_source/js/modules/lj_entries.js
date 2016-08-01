var React = require('react');
var moment = require('moment');

var LJPaginator = React.createClass({
    getDefaultProps: function () {
        return {paginator: 'foo'}
    },

    addPaginationMarkup: function() { return {__html: this.props.paginator}; },

    render: function() {
        var pagination = this.props.paginator;
        return (
            <div className="pagination" dangerouslySetInnerHTML={this.addPaginationMarkup()}/>
        );
    }
});

var LJByline = React.createClass({
    getDefaultProps: function() {
        return {entry: {}}
    },

    localizeTime: function(timeString) {
        var utctime = moment.utc(timeString);
        var time = moment(utctime.toDate());
        return time.format('dddd, D MMMM, YYYY, h:mm a');
    },

    format_courses: function(author_data) {
        return author_data.course_id.join(', ');
    },

    render: function() {
        var entry = this.props.entry,
            author = entry ? entry.author : {},
            display_name = author ? author.display_name : '',
            user_name = author ? author.username : '',
            author_name = display_name || user_name || 'anonymous',
            created = entry ? entry.created : '';

        return (
            <div className="byline">
                By <span className="author">{author_name}</span>
                   <span className="courses"> ({this.format_courses(author)}) </span>
                   &mdash; {this.localizeTime(created)}
            </div>
        );
    }
});

var LJEntry = module.exports.LJEntry = React.createClass({
    getDefaultProps: function() {
        return {entry: {}, user: {}, title_link: false}
    },

    getEntryText: function() {
        var entry = this.props.entry;
        if (entry.markdown) {
            return {__html: entry.markdown};
        } else {
            return {__html: entry.text};
        }
    },

    render: function() {
        var entry = this.props.entry,
            title = entry ? entry.title : '',
            url = entry ? entry.url : '',
            actions = entry ? entry.actions : {},
            edit_url = actions ? actions.edit : '',
            delete_url = actions ? actions.delete : '';
        return (
            <article>
                <h2>
                    {this.props.title_link ? <a href={url} title={title}>{title}</a> : <span>{title}</span>}
                </h2>
                <LJByline entry={entry} />
                <div className="entryBody" dangerouslySetInnerHTML={this.getEntryText()}/>
                {edit_url && <a className="btn btn-primary" href={edit_url} title="Edit this entry">Edit</a>}
                {delete_url && <a className="btn btn-danger pull-right" href={delete_url} title="Delete this entry">Delete</a>}
            </article>
        );
    }
});


var LJEntryList = module.exports.LJEntryList = React.createClass({
    getDefaultProps: function() {
        return {entries: [], user: {}, pagination: ''};
    },

    render: function() {
        var entries = this.props.entries;
        var user = this.props.user;
        var pagination = this.props.pagination;
        return (
            <div className="entryList">
                {(entries.length > 5) && pagination && <LJPaginator paginator={pagination} />}
                {entries.map(entry => <LJEntry key={entry.id} entry={entry} user={user} title_link={true} />)}
                {pagination && <LJPaginator paginator={pagination} />}
            </div>
        );
    }
});