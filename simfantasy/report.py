import json
import glob
from simfantasy.enums import Race
class Report:
    def __init__(self, sim):
        self.actors = sim.actors
        self.sim = sim
    def render(self):
        stats = self.parse_actors()
        html = """
        <html>
          <head>
            <title>Simfantasy Report</title>
            <meta charset="UTF-8">
            <script type="text/javascript">
               window.actor_data = {}.reverse();
            </script>
          </head>
          <body>
            <div id='root'></div>
        """.format(json.dumps(stats))
        javascript = ""
        file = glob.glob('./reporting/build/static/js/*.js')[0]
        with open(file, 'r') as fin:
            javascript = fin.read()
        html += """
            <script type="text/javascript">
              {}
            </script>
        """.format(javascript)
        css = ""
        file = glob.glob('./reporting/build/static/css/*.css')[0]
        with open(file, 'r') as fin:
            css = fin.read()
        html += """
            <style>
              {}
            </style>
        """.format(css)
        html += """
          </body>
        </html>
        """
        file = open("./report.html","w")
        file.write(html)
        file.close()
    def parse_actors(self):
        actors = self.actors
        results = []
        for actor in actors:
            actions = {}
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
            results.append({
                'name': actor.name,
                # 'job': actor.job.name,
                'level': actor.level,
                'race': actor.race.name,
                'combatLength': self.sim.combat_length.total_seconds(),
                'actions': actions,
            })
        return results
