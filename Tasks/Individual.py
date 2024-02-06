#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import argparse
import os
import logging
import xml.etree.ElementTree as ET
from typing import List


@dataclass
class Student:
    name: str
    group: int
    grade: str


def add_student(students: List[Student], name: str, group: int, grade: str) -> List[Student]:
    """
    Добавить данные о студенте
    """
    students.append(Student(name, group, grade))
    return students


def show_list(students: List[Student]):
    """
    Вывести список студентов
    """
    if students:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)

        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.name,
                    student.group,
                    student.grade
                )
            )
        print(line)
    else:
        print("Список студентов пуст.")


def show_selected(students: List[Student]) -> List[Student]:
    result = []
    for student in students:
        grade = [int(x) for x in student.grade.split()]
        if sum(grade) / max(len(grade), 1) >= 4.0:
            result.append(student)
    return result


def save_students(file_name: str, students: List[Student]):
    """
    Сохранение данных в XML
    """
    root = ET.Element("students")
    for student in students:
        student_element = ET.SubElement(root, "student")
        ET.SubElement(student_element, "name").text = student.name
        ET.SubElement(student_element, "group").text = str(student.group)
        ET.SubElement(student_element, "grade").text = student.grade

    tree = ET.ElementTree(root)
    tree.write(file_name, encoding="utf-8", xml_declaration=True)


def load_students(file_name: str) -> List[Student]:
    """
    Загрузка данных из XML
    """
    students = []
    if not os.path.exists(file_name):
        return students

    tree = ET.parse(file_name)
    root = tree.getroot()

    for student_element in root.findall("student"):
        students.append(
            Student(
                name=student_element.find("name").text,
                group=int(student_element.find("group").text),
                grade=student_element.find("grade").text
            )
        )
    return students


def main(command_line=None):
    logging.basicConfig(
        filename="students.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="UTF-8",
    )

    parser = argparse.ArgumentParser(description="Students management system")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    subparsers = parser.add_subparsers(dest="command", help="commands")

    # Add student command
    add_parser = subparsers.add_parser("add", help="Add a new student")
    add_parser.add_argument("--file", required=True, help="Path to the data file")
    add_parser.add_argument("-n", "--name", required=True, help="Student's name")
    add_parser.add_argument("-g", "--group", required=True, type=int, help="Student's group")
    add_parser.add_argument("-gr", "--grade", required=True, help="Student's grade")

    # Display command
    display_parser = subparsers.add_parser("display", help="Display all students")

    # Select command
    select_parser = subparsers.add_parser("select", help="Select students with grade >= 4.0")

    # Save command
    save_parser = subparsers.add_parser("save", help="Save students list to file")
    save_parser.add_argument("-f", "--file", required=True, help="File name to save")

    # Load command
    load_parser = subparsers.add_parser("load", help="Load students list from file")
    load_parser.add_argument("-f", "--file", required=True, help="File name to load")

    args = parser.parse_args(command_line)

    if args.command == "add":
        if not os.path.exists(args.file):
            students = []
        else:
            students = load_students(args.file)
        students = add_student(students, args.name, args.group, args.grade)
        save_students(args.file, students)

    elif args.command == "display":
        if os.path.exists(args.file):
            students = load_students(args.file)
            show_list(students)
        else:
            print("No data file found.")

    elif args.command == "select":
        if os.path.exists(args.file):
            students = load_students(args.file)
            selected_students = show_selected(students)
            show_list(selected_students)
        else:
            print("No data file found.")

    elif args.command == "save":
        if os.path.exists(args.file):
            students = load_students(args.file)
            save_students(args.file, students)
        else:
            print("No data to save.")

    elif args.command == "load":
        if os.path.exists(args.file):
            students = load_students(args.file)
            show_list(students)
        else:
            print("File not found.")


if __name__ == '__main__':
    main()
