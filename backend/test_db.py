from event_tracker import save_event, get_events

# Force a test event
save_event(["Text: Test dream"], "This is a test dream description.")

# Fetch events
events = get_events(limit=5)
print("Events in DB:", events)
