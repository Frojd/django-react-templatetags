from django.shortcuts import render


def menu_view(request):
    return render(
        request,
        "examplesite/index.html",
        {
            "menu_data": {
                "example": 1,
            },
        },
    )
