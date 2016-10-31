angular.module('myApp').directive('treednd', function () {
    return {
        restrict: 'EA',
        link: function (scope, elt, attrs) {
            elt.draggable({
                cursor: 'move',
                appendTo: 'body',
                disabled: !scope.$parentNode,
                drag: function (event, ui) {
                    var destination = ui.helper.data('destination')
                        if (destination) {
                            var cursorPos = event.pageY;
                            var destPos = destination.offset().top;
                            var offset = cursorPos - destPos;
                            var h = destination.height();

                            var position;
                            if (offset <= h / 3) {
                                position = 'up';
                            } else if (offset >= 2 * h / 3) {
                                position = 'down';
                            } else {
                                position = 'middle';
                            }
                            ui.helper.data('position', position);
                            destination.removeClass('hover-up hover-middle hover-down');
                            destination.addClass('hover-' + position);
                        }
                },
                helper: function (event) {
                    var helper = $('<div class="helper">' + scope.node.name + '</div>');
                    // fill some data to be catched up by droppable() of receiver directives
                    helper.data('node', scope.node);
                    helper.data('parentNode', scope.$parentNode);
                    return helper;
                }

            });
            elt.droppable({
                tolerance: 'pointer',
                over: function (event, ui) {
                    ui.helper.data('destination', elt);
                    elt.addClass('hover');
                },
                out: function (event, ui) {
                    ui.helper.data('destination', null);
                    elt.removeClass('hover hover-up hover-middle hover-down');
                },
                drop: function (event, ui) {
                    var toNode = scope.node;
                    var toParent = scope.$parentNode ? scope.$parentNode.children : null;
                    var fromNode = ui.helper.data('node');
                    var fromParentNode = ui.helper.data('parentNode');
                    var position = ui.helper.data('position');

                    scope.$apply(function () {
                        var idx;
                        if (fromParentNode) {
                            idx = fromParentNode.children.indexOf(fromNode);
                            if (idx != -1) {
                                fromParentNode.children.splice(idx, 1);
                            }
                        }
                        if (position === 'middle') {
                            if (toNode.children) {
                                // inside
                                if(toNode.type === 'file'){
                                    if (toParent) {
                                        idx = toParent.indexOf(toNode);
                                        toParent.splice(idx + 1, 0, fromNode);
                                    }
                                } else {
                                    toNode.children.push(fromNode);
                                }
                            }
                        } else if (position === 'up') {
                            if (toParent) {
                                idx = toParent.indexOf(toNode);
                                toParent.splice(idx, 0, fromNode);
                            }
                        } else if (position === 'down') {
                            if (toParent) {
                                idx = toParent.indexOf(toNode);
                                toParent.splice(idx + 1, 0, fromNode);
                            }
                        }
                    });
                    elt.removeClass('hover hover-up hover-middle hover-down');

                }
            });

            var dereg = scope.$on('$destroy', function () {
                try {
                    elet.draggable('destroy');
                } catch (e) {
                    // may fail
                }
                dereg();
                dereg = null;
            });
        }
    };
});
