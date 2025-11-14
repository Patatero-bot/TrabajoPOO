from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from DAO.Conexion import ConexionBD

class ExportadorPDF:
    @staticmethod
    def generar_informe_empleados(conexion: ConexionBD, filename="informe_empleados.pdf"):
        try:
            empleados = conexion.ejecutar(
                """
                SELECT p.nombre_completo, p.cargo, p.salario, p.email, p.fono, d.nombre as departamento, p.fecha_inicio
                FROM persona p LEFT JOIN departamento d ON p.iddepartamento = d.iddepartamento
                ORDER BY d.nombre, p.nombre_completo
                """
            ).fetchall()
            if not empleados:
                print("No hay empleados.")
                return False
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            st = getSampleStyleSheet()
            elements += [Paragraph("INFORME DE EMPLEADOS - ECOTECH SOLUTIONS", st['Title']), Spacer(1, 0.2*inch)]
            elements += [Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", st['Normal']), Spacer(1, 0.3*inch)]
            data = [['Nombre', 'Cargo', 'Salario', 'Departamento', 'Teléfono', 'Email']]
            for e in empleados:
                data.append([e['nombre_completo'], e['cargo'], f"${e['salario']:,}", e['departamento'] or 'Sin asignar', e['fono'], e['email']])
            table = Table(data, colWidths=[1.5*inch, 1.2*inch, 1*inch, 1.2*inch, 1*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            elements += [table, Spacer(1, 0.2*inch)]
            elements += [Paragraph(f"Total de empleados: {len(empleados)}", st['Normal'])]
            doc.build(elements)
            print(f"PDF generado: {filename}")
            return True
        except Exception as e:
            print(f"Error PDF: {e}")
            return False

    @staticmethod
    def generar_informe_proyectos(conexion: ConexionBD, filename="informe_proyectos.pdf"):
        try:
            proyectos = conexion.ejecutar(
                """
                SELECT p.nombre, p.descripcion, d.nombre as departamento, COUNT(ip.idpersona) as empleados_asignados
                FROM proyecto p LEFT JOIN departamento d ON p.iddepartamento = d.iddepartamento
                LEFT JOIN inscripcion_proyecto ip ON p.idproyecto = ip.idproyecto
                GROUP BY p.idproyecto ORDER BY d.nombre, p.nombre
                """
            ).fetchall()
            if not proyectos:
                print("No hay proyectos.")
                return False
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            st = getSampleStyleSheet()
            elements += [Paragraph("INFORME DE PROYECTOS - ECOTECH SOLUTIONS", st['Title']), Spacer(1, 0.2*inch)]
            elements += [Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", st['Normal']), Spacer(1, 0.3*inch)]
            data = [['Proyecto', 'Descripción', 'Departamento', 'Empleados Asignados']]
            for p in proyectos:
                data.append([p['nombre'], p['descripcion'], p['departamento'] or 'Sin asignar', str(p['empleados_asignados'])])
            table = Table(data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            elements.append(table)
            doc.build(elements)
            print(f"PDF proyectos generado: {filename}")
            return True
        except Exception as e:
            print(f"Error PDF proyectos: {e}")
            return False