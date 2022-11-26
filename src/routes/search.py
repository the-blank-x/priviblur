import urllib.parse

import dominate
import sanic
import sanic_ext

import npf_renderer
import privblur_extractor

search = sanic.Blueprint("search", url_prefix="/search")


async def render_results(initial_results, query, url_handler):
        timeline = privblur_extractor.parse_container(initial_results)

        return await sanic_ext.render(
            "search.jinja",
            context={
                "timeline": timeline,
                "query": query,
                "url_handler": url_handler,
                "format_npf": npf_renderer.format_npf
            }
        )


@search.get("/<query:str>")
async def _main(request: sanic.Request, query: str):
    query = urllib.parse.unquote(query)
    timeline_type = request.app.ctx.TumblrAPI.config.TimelineType

    initial_results = await request.app.ctx.TumblrAPI.timeline_search(query, timeline_type.POST)
    return await render_results(initial_results, query, request.app.ctx.URL_HANDLER)