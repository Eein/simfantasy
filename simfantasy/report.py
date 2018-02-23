import json
import jsonpickle

class Report:
    def __init__(self, actors: None):
        self.actors = actors
    def render(self):
        stats = self.parse_actors()
        html = """
        <html>
          <head>
            <title>Simfantasy Report</title>
            <script src="https://cdn.jsdelivr.net/npm/vue"></script>
            <script type="text/javascript">
               window.actor_data = {};
            </script>
          </head>
          <body>
          </body>
        </html>
        """.format(json.dumps(stats))
        file = open("./report.html","w")
        file.write(html)
        file.close()
    def parse_actors(self):
        actors = self.actors
        actions = {}
        for actor in actors:
            for cls in actor.statistics['actions']:
                actions[cls.__name__] = actor.statistics['actions'][cls]
        for action in actions:
            for k,v in enumerate(actions[action]['casts']):
                actions[action]['casts'][k] = v.timestamp()
            for k,v in enumerate(actions[action]['execute_time']):
                actions[action]['execute_time'][k] = { 'time': v[0].timestamp(), 'delta': v[1].total_seconds() }
            for k,v in enumerate(actions[action]['damage']):
                actions[action]['damage'][k] = { 'time': v[0].timestamp(), 'damage': v[1] }
            for k,v in enumerate(actions[action]['critical_hits']):
                actions[action]['critical_hits'][k] = v.timestamp()
            for k,v in enumerate(actions[action]['direct_hits']):
                actions[action]['direct_hits'][k] = v.timestamp()
            for k,v in enumerate(actions[action]['critical_direct_hits']):
                actions[action]['critical_direct_hits'][k] = v.timestamp()
        return {
            'actions': actions
        }
