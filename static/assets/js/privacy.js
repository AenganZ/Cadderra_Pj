document.addEventListener('DOMContentLoaded', function() {
    let Accordion = document.querySelectorAll('.accordion--wrapper');
    let Triggers = [], Contents = [];
    let animation, close;

    if(Accordion.length > 0) {
        for(let i = 0; i < Accordion.length; i++) {
            Triggers[i] = Accordion[i].querySelectorAll('.accordion--trigger');
            Contents[i] = Accordion[i].querySelectorAll('.accordion--content');

            if(Triggers[i].length > 0) {
                for(let j = 0; j < Triggers[i].length; j++) {
                    _clickEvent(Triggers[i][j], i, j);
                }
            }
            if(Contents[i].length > 0) {
                for(let j = 0; j < Contents[i].length; j++) {
                    if(!Contents[i][j].classList.contains('accordion--active')) {
                        Contents[i][j].style.height = 0;
                    }
                }
            }
        }

        animation = function(el, type) {
            if(type == "open") {
                el.classList.add("accordion--active");
                el.style.height = 'auto';
                let height = el.clientHeight;
                el.style.height = 0;

                anime({
                    targets: el,
                    height: [0, height],
                    duration: 500,
                    easing: 'easeOutExpo',
                    complete: function() {
                        el.style.height = 'auto';
                    }
                });
            } else {
                anime({
                    targets: el,
                    height: 0,
                    duration: 500,
                    easing: 'easeOutExpo',
                    complete: function() {
                        el.classList.remove("accordion--active");
                    }
                });
            }
        };

        close = function(i) {
            let triggerActive = Accordion[i].querySelector('.accordion--trigger.accordion--active');
            if(triggerActive) {
                triggerActive.classList.remove('accordion--active');
            }
            let contentActive = Accordion[i].querySelector('.accordion--content.accordion--active');
            if(contentActive) {
                contentActive.classList.remove('accordion--active');
                animation(contentActive, 'close');
            }
        };

        function _clickEvent(el, i, index) {
            el.addEventListener('click', function(e) {
                e.preventDefault();

                if(Contents[i][index]) {
                    if(!Contents[i][index].classList.contains('accordion--active')) {
                        close(i);
                        e.target.classList.add('accordion--active');
                        animation(Contents[i][index], 'open');
                    } else {
                        close(i);
                    }
                }
            });
        }
    }
});
