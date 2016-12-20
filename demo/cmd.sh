# To receive all the logs run:
$ python routing.py "#"

#To receive all logs from the facility "kern":
$ python routing.py "kern.*"

# Create tree consumers
$ python routing.py "DNA.*"
$ python routing.py "AGDREF.*"
$ python routing.py "INEREC.*"

# Or if you want to hear only about "critical" logs:
$ python routing.py "*.critical"

# You can create multiple bindings:
$ python routing.py "kern.*" "*.critical"

# And to emit a log with a routing key "kern.critical" type:
$ python emit_log_topic.py "kern.critical" "A critical kernel error"
$ python emit_log_topic.py "DNA.mise_a_jour" "Avertir DNA de la MAJ"
