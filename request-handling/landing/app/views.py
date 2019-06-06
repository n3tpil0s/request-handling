from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing

    if request.GET.get('from-landing') == 'original':
        counter_click['original'] += 1
    elif request.GET.get('from-landing') == 'test':
        counter_click['test'] += 1

    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    landing_org_html = 'landing.html'
    landing_alt_html = 'landing_alternate.html'

    render_page = landing_org_html if request.GET.get('ab-test-arg') == 'original' else landing_alt_html
    print(render_page)
    if render_page == landing_org_html:
        counter_show['original'] += 1
    else:
        counter_show['test'] += 1

    return render_to_response(render_page)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    try:
        test_counter = counter_click["test"] / counter_show["test"]
    except ZeroDivisionError:
        test_counter = 0.0

    try:
        orig_counter = counter_click["original"] / counter_show["original"]
    except ZeroDivisionError:
        orig_counter = 0.0

    return render_to_response('stats.html', context={
        'test_conversion': test_counter,
        'original_conversion': orig_counter,
    })
