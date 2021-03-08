import argparse
import json
import matplotlib.pyplot as plt

FILE_LOCATION = 'data/inputs/input.json'

parser = argparse.ArgumentParser(description='Finds the number of classrooms needed to schedule the list of class '
                                             'times provided')
parser.add_argument('-f', action='store', dest='schedule_location', help='Relative path to input file',
                    default=FILE_LOCATION)


def get_schedule(class_times):
    sorted_times = sorted(class_times, key=lambda x: x[0])

    classroom_list = []
    remaining_times = sorted_times

    while remaining_times:

        classroom_list.append([])
        classroom = classroom_list[-1]
        conflict_times = []

        previous_interval = remaining_times[0]
        classroom.append(previous_interval)

        for current_interval in remaining_times[1:]:
            # They don't overlap
            if current_interval[0] >= previous_interval[1]:
                classroom.append(current_interval)
                previous_interval = current_interval

            # They conflict so you need a new classroom
            else:
                conflict_times.append(current_interval)

        # Classes that haven't been scheduled are remaining
        remaining_times = conflict_times

    return classroom_list


# Draws Gantt chart from intervals assigned each classroom.
def draw_gantt(classrooms_schedule):
    fig, gnt = plt.subplots()

    x_max = classrooms_schedule[0][-1][1]
    for classroom_schedule in classrooms_schedule[1:]:
        tmp = classroom_schedule[-1][1]
        if tmp > x_max:
            x_max = tmp

    gnt.set_ylim(0, 15 * len(classrooms_schedule) + 15)
    gnt.set_xlim(0, x_max + 10)

    y_shift = 10

    gnt.set_xlabel('Time (t)')
    gnt.set_ylabel('Classrooms')

    gnt.set_yticks([(i + 1) * 10 + 5 for i in range(len(classrooms_schedule))])
    gnt.set_yticklabels([str(i + 1) for i in range(len(classrooms_schedule))])

    gnt.grid(True)

    for classroom_schedule in classrooms_schedule:
        times = []
        names = []
        for interval in classroom_schedule:
            times.append((interval[0], interval[1] - interval[0]))
            names.append(interval[2])

        gnt.broken_barh(times, (y_shift, 9), edgecolor='black', linewidth=2, facecolor='yellow')

        for class_name, pair in zip(names, times):
            gnt.text(x=pair[0] + pair[1] / 2,
                     y=y_shift + 5,
                     s=class_name,
                     ha='center',
                     va='center',
                     color='black',
                     )
        y_shift += 10

    plt.show(block=True)


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.schedule_location) as f:
        schedule = json.load(f)['times']

        classrooms_schedule = get_schedule(schedule)
        print('Number of classrooms required: {}'.format(len(classrooms_schedule)))
        draw_gantt(classrooms_schedule)
