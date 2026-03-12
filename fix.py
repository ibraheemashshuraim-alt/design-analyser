import re

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Expose Firebase to window in the module script
    module_script_replacement = """
        let app, auth, db;
        try {
            app = initializeApp(firebaseConfig);
            auth = getAuth(app);
            db = getFirestore(app);
            
            // Expose to window for the main script
            window.app = app;
            window.auth = auth;
            window.db = db;
            window.onAuthStateChanged = onAuthStateChanged;
            window.signInWithPopup = signInWithPopup;
            window.GoogleAuthProvider = GoogleAuthProvider;
            window.doc = doc;
            window.setDoc = setDoc;
            window.getDoc = getDoc;
            window.updateDoc = updateDoc;
            window.onSnapshot = onSnapshot;
            window.collection = collection;
            window.query = query;
            window.where = where;
            window.getDocs = getDocs;
            window.increment = increment;
            window.addDoc = addDoc;
            window.orderBy = orderBy;
            window.limit = limit;
            
            // Compatibility object for inline HTML calls
            window.firebase = {
                auth: () => ({
                    signOut: () => signOut(auth),
                    get currentUser() { return auth.currentUser; }
                }),
                firestore: () => ({
                    collection: (coll) => ({
                        doc: (dId) => ({
                            onSnapshot: (cb) => onSnapshot(doc(db, coll, dId), cb),
                            set: (data) => setDoc(doc(db, coll, dId), data),
                            update: (data) => updateDoc(doc(db, coll, dId), data)
                        })
                    })
                })
            };
            console.log("Firebase initialized modularly and exposed globally.");
        } catch (e) { console.error("Firebase Initialization Error.", e); }
"""

    orig_module_catch = """
        let app, auth, db;
        try {
            app = initializeApp(firebaseConfig);
            auth = getAuth(app);
            db = getFirestore(app);
            console.log("Firebase initialized modularly");
        } catch (e) { console.error("Firebase Initialization Error.", e); }
"""
    # Replace whitespace smartly
    content = content.replace(orig_module_catch.strip(), module_script_replacement.strip())
    # If it failed to replace because of exact formatting, use regex
    if module_script_replacement.strip() not in content:
        content = re.sub(r'let app, auth, db;.*?catch \(e\) \{ console\.error\("Firebase Initialization Error\.", e\); \}', module_script_replacement.strip(), content, flags=re.DOTALL)


    # 2. Add aliases at the beginning of the second script block
    alias_block = """
        // Re-bind global firebase modular functions to local scope for compat
        const auth = window.auth;
        const db = window.db;
        const onAuthStateChanged = window.onAuthStateChanged;
        const signInWithPopup = window.signInWithPopup;
        const GoogleAuthProvider = window.GoogleAuthProvider;
        const doc = window.doc;
        const setDoc = window.setDoc;
        const getDoc = window.getDoc;
        const updateDoc = window.updateDoc;
        const onSnapshot = window.onSnapshot;
        const collection = window.collection;
        const query = window.query;
        const where = window.where;
        const getDocs = window.getDocs;
        const increment = window.increment;
        const addDoc = window.addDoc;
        const orderBy = window.orderBy;
        const limit = window.limit;
    """

    # We want to put it right after `<script>\n        const dropZone = document.getElementById('dropZone');`
    content = content.replace("const dropZone = document.getElementById('dropZone');", alias_block + "\n        const dropZone = document.getElementById('dropZone');")


    # 3. Add missing login and export functions just before `// ================ FIREBASE AUTH ================`
    added_funcs = """
        window.loginWithGoogle = async function() {
            try {
                const provider = new GoogleAuthProvider();
                await signInWithPopup(auth, provider);
            } catch (error) {
                console.error("Login Error:", error);
                alert("لاگ ان میں مسئلہ پیش آیا: " + error.message);
            }
        };

        window.exportPrint = function() {
            window.print();
        };

        window.exportPNG = async function() {
            const panel = document.getElementById('resultsPanel');
            const canvas = await html2canvas(panel, { scale: 2, useCORS: true, backgroundColor: '#0a1320' });
            const link = document.createElement('a');
            link.download = 'DesignCheck-Report.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        };

        window.exportPDF = async function() {
            const panel = document.getElementById('resultsPanel');
            const canvas = await html2canvas(panel, { scale: 2, useCORS: true, backgroundColor: '#0a1320' });
            const imgData = canvas.toDataURL('image/png');
            let pdf;
            if (canvas.width > canvas.height) {
                pdf = new jspdf.jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
            } else {
                pdf = new jspdf.jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
            }
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save('DesignCheck-Report.pdf');
        };

        // ================ FIREBASE AUTH ================
"""
    content = content.replace("// ================ FIREBASE AUTH ================", added_funcs.strip())

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix()
print("Applied fixes to index.html successfully.")
